import { Injectable } from '@angular/core';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';
import { retryWhen, tap, delay } from 'rxjs/operators';
import { Observable } from 'rxjs';

export interface Protocol{
  type: string;
  msg?: any;
}
export interface JobInfo extends Protocol{
  msg: Job;
}
export interface Job{
  code?: string;
  vars?: string;
  history?: [];
  name?: string;
}

export interface Hosts extends Protocol{
  msg: Host;
}
export interface Host{
  master: string;
  servers: [];
}

@Injectable({
  providedIn: 'root'
})
export class WebSocketService {
  ws: WebSocketSubject<any> ;

  // currentJob: JobInfo = {type:"job", msg:{}}
  currentJob$: Observable<JobInfo>;

  constructor() {
    this.ws = webSocket('ws:/127.0.0.1:5124'); // 95.24.211.79
    this.ws.subscribe();
  }

  getObservable(subscribeType){
    return this.ws.multiplex(
      () => {
        console.log('Try sub: ', subscribeType);
        return (subscribeType);
      },
      () => {
        console.log('Unsub: ', subscribeType);
        return ( {type: 'unsubscribe', msg: subscribeType.type} );
      },
      (message) => {
         if (message.type === subscribeType.type){
           console.log('Subbed: ', subscribeType);
         }
         return message.type === subscribeType.type;
      }
    ).pipe(
      retryWhen(errors =>
        errors.pipe(
          tap(err => {
            console.error('Got error for subscribe: ', subscribeType, err);
            // this.ws.unsubscribe();
            this.ws = webSocket('ws:/127.0.0.1:5124'); // 95.24.211.79
            this.ws.subscribe();
          }),
          delay(1000)
        )
      )
    );
  }

  sendMessage(message){
    this.ws.next(message);
    console.log(message);
  }

  ngOnDestroy(){
    this.ws.unsubscribe();
  }

}
