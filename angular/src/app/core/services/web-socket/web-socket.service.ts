import { Injectable } from '@angular/core';
import { webSocket, WebSocketSubject } from "rxjs/webSocket";
import { retryWhen, tap, delay } from 'rxjs/operators';
import { Observable } from 'rxjs';

export interface Protocol{
  type: string
  msg?: any
}
export interface JobInfo extends Protocol{
  msg: Job
}
export interface Job{
  code?: string,
  vars?: string,
  history?: [],
  name?: string
}

@Injectable({
  providedIn: 'root'
})
export class WebSocketService {
  ws: WebSocketSubject<any> ;

  currentJob: JobInfo = {type:"job", msg:{}}
  currentJob$: Observable<JobInfo>

  constructor() {
    this.ws = webSocket('ws:/95.24.211.79:8123') //95.24.211.79
    this.ws.subscribe()
  }

  getObservable(subscribeType: Protocol){
    return this.ws.multiplex(
      () => {
        console.log("Try sub: ", subscribeType)
        return (subscribeType)
      },
      () => {
        console.log("Unsub: ", subscribeType)
        return ( {type: "unsubscribe", msg: subscribeType.type} )
      },
      (message: Protocol) => {
         if (message.type === subscribeType.type){
           console.log("Subbed: ", subscribeType)
         }
         return message.type === subscribeType.type
      }
    ).pipe(
      retryWhen(errors =>
        errors.pipe(
          tap(err => {
            console.error('Got error for subscribe: ', subscribeType, err);
          }),
          delay(1000)
        )
      )
    )
  }

  sendMessage(message){
    this.ws.next(message)
  }

  ngOnDestroy(){
    this.ws.unsubscribe()
  }

}
