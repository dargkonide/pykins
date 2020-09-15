import { Injectable } from '@angular/core';
import { Observable, Subscription, timer } from 'rxjs';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';
import { delayWhen, retryWhen, tap } from 'rxjs/operators';

const IP: string = 'ws:/127.0.0.1:5124'; // 95.24.211.79
const RECONNECT_DELAY_SEC: number = 5;

@Injectable({
  providedIn: 'root',
})
export class WebSocketService {
  ws: WebSocketSubject<any>;
  ws$: Subscription;
  currentJob$: Observable<any>;

  constructor() {
    // https://rxjs-dev.firebaseapp.com/api/webSocket/webSocket
    // https://rxjs-dev.firebaseapp.com/api/webSocket/WebSocketSubjectConfig
    this.ws = webSocket({
      url: IP,
      openObserver: {
        next: () => {
          console.debug(`WebSocket '${IP}' connected.`);
        },
      },
    });
  }

  sendMessage(message) {
    this.ws.next(message);
    console.debug('Send message: \n', message);
  }

  getObservable(subscribeType: { type: string }): Observable<any> {
    return this.ws
      .multiplex(
        () => {
          console.debug('Try sub: \n', subscribeType);
          return subscribeType;
        },
        () => {
          console.debug('Unsub: \n', subscribeType);
          return { type: 'unsubscribe', msg: subscribeType.type };
        },
        (message: { type: string }) => {
          if (message.type === subscribeType.type) {
            console.debug('Subbed: \n', subscribeType);
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
            //log error message
            tap(() => console.debug(`WebSocket '${IP}' disconnected.`)),
            //restart in 5 seconds
            delayWhen(() => timer(RECONNECT_DELAY_SEC * 1000))
          )
        )
      );
  }
}
