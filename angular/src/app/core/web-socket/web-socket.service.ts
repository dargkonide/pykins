import { Injectable } from '@angular/core';
import { webSocket, WebSocketSubject } from "rxjs/webSocket";
import { retryWhen, tap, delay } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class WebSocketService {
  ws: WebSocketSubject<any> ;

  constructor() {
    this.ws = webSocket('ws:/95.24.211.79:8123')
    this.ws.subscribe()
  }

  getObservable(subscribeType: String){
    return this.ws.multiplex(
      () => ({subscribe: subscribeType}),
      () => ({unsubscribe: subscribeType}),
      (message) => message.type === subscribeType
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
