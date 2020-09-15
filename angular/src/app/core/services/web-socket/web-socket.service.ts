import { Injectable } from '@angular/core';
import { Observable, Subscription, timer } from 'rxjs';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';
import {delay, delayWhen, retryWhen, tap} from 'rxjs/operators';
import {ActivatedRoute, Router} from '@angular/router';

const IP = 'ws:/127.0.0.1:5124'; // 95.24.211.79
const RECONNECT_DELAY_SEC = 5;

export interface subscribeType{
  type: string;
  [propName: string]: any;
}

@Injectable({
  providedIn: 'root',
})
export class WebSocketService {
  ws: WebSocketSubject<any>;

  constructor(private router: Router,
              private route: ActivatedRoute) {
    // https://rxjs-dev.firebaseapp.com/api/webSocket/webSocket
    // https://rxjs-dev.firebaseapp.com/api/webSocket/WebSocketSubjectConfig
    this.ws = webSocket({
      url: IP,
      openObserver: {
        next: () => {
          console.log(`WebSocket '${IP}' connected.`);
        },
      },
    });
    this.ws.subscribe();
  }

  sendMessage(message) {
    this.ws.next(message);
    console.log('Send message: \n', message);
  }

  getObservable(subscribeType): Observable<any> {
    return this.ws
      .multiplex(
        () => {
          console.log('Try sub: \n', subscribeType);
          return subscribeType;
        },
        () => {
          console.log('Unsub: \n', subscribeType);

          return { type: 'unsubscribe', msg: subscribeType.type };
        },
        (message: { type: string }) => {
          if (message.type === subscribeType.type) {
            console.log('Subbed: \n', subscribeType);
          }
          return message.type === subscribeType.type;
        }
      )
      .pipe(
        // https://www.learnrxjs.io/learn-rxjs/operators/error_handling/retrywhen
        retryWhen((errors) =>
          errors.pipe(
            // log error message
            tap(() => {
              this.ws.unsubscribe();
              this.ws = webSocket({
                url: IP,
                openObserver: {
                  next: () => {
                    console.log(`WebSocket '${IP}' connected.`);
                  },
                },
              });
              this.ws.subscribe();
              if (this.router.url==='/jobs') this.router.navigate(['/hosts'])
              else this.router.navigate(['/jobs'])
              }),
            // restart in 5 seconds
              delayWhen(() => timer(RECONNECT_DELAY_SEC * 1000))
          )
        )
      );
  }
}
