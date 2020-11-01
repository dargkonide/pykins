import { Injectable } from '@angular/core';
import { Observable, Subscription, timer } from 'rxjs';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';
import { delayWhen, map, retryWhen, tap } from 'rxjs/operators';
import { IAuth } from '../auth/model/user';

export interface Protocol {
  type: string;
  token?: string
  error?: string
  msg?: any;
  [params: string]: any;
}

const CONN_STR = 'ws:/85.249.192.240:5124'; // 95.24.211.79
const RECONNECT_DELAY_SEC = 5;

@Injectable({
  providedIn: 'root',
})
export class WebSocketService {
  private ws$: WebSocketSubject<any>;
  private wsSub: Subscription;
  public currentJob$: Observable<any>;

  constructor() {
    this.connect();
  }
  connect(): void {
    // https://rxjs-dev.firebaseapp.com/api/webSocket/webSocket
    if (!this.ws$ || this.ws$.closed) {
      this.ws$ = webSocket({
        url: CONN_STR,
        openObserver: {
          next: (Event) => {
            console.debug(`WebSocket '${CONN_STR}' connected. \n`, Event);
          },
        },
        closeObserver: {
          next: (closeEvent) => {
            console.debug(
              `WebSocket '${CONN_STR}' disconnected. \n`,
              closeEvent
            );
          },
        },
        closingObserver: {
          next: (ss) => {
            console.debug(`WebSocket '${CONN_STR}' closing Observer. \n`, ss);
          },
        },
      });
      // need for 1 connect on all session, without this all pages will reconnect per request
      this.wsSub = this.ws$
        .pipe(
          // https://www.learnrxjs.io/learn-rxjs/operators/error_handling/retrywhen
          retryWhen((errors) =>
            errors.pipe(
              // log error message
              tap(() =>
                console.debug(`WebSocket '${CONN_STR}' trying reconnect`)
              ),
              // restart in 5 seconds
              delayWhen(() => timer(RECONNECT_DELAY_SEC * 1000))
            )
          )
        )
        .subscribe();
    }
  }
  disconnect(): void {
    this.wsSub.unsubscribe();
    this.ws$.complete();
    this.ws$ = null;
  }

  sendMessage(message: Protocol): void {
    this.ws$.next(message);
    console.debug('Send message: \n', message);
  }
  getObservable(subscribeType: Protocol): Observable<Protocol> {
    return this.ws$
      .multiplex(
        () => {
          console.debug(`Subscribe to type '${subscribeType.type}'.`);
          return subscribeType;
        },
        () => {
          console.debug(`Unsubscribe to type '${subscribeType.type}'.`);
          return { type: 'unsubscribe', msg: subscribeType.type };
        },
        (message: { type: string }) => {
          if (message.type === subscribeType.type) {
            console.debug(
              `Get msg for type '${subscribeType.type}'. \n`,
              message
            );
            return true;
          } else {
            return false;
          }
        }
      )
      .pipe(
        // https://www.learnrxjs.io/learn-rxjs/operators/error_handling/retrywhen
        retryWhen((errors) =>
          errors.pipe(
            // log error message
            tap(() =>
              console.debug(
                `WebSocket '${CONN_STR}' trying reconnect for type '${subscribeType.type}'`
              )
            ),
            // restart in 5 seconds
            delayWhen(() => timer(RECONNECT_DELAY_SEC * 1000))
          )
        )
      );
  }
}
