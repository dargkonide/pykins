import { Injectable } from '@angular/core';
import { webSocket, WebSocketSubject } from "rxjs/webSocket";
import { Subscription } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class WebSocketService {
  ws: WebSocketSubject<any> ;
  wsSender: Subscription;

  constructor() {
    this.ws = webSocket('ws://95.24.211.79:8123');
    this.ws.subscribe()
  }

  getObservable(subscribeType: String){
    return this.ws.multiplex(
      () => ({subscribe: subscribeType}),
      () => ({unsubscribe: subscribeType}),
      (message) => message.type === subscribeType
    );
  }

  sendMessage(message){
    this.ws.next(message)
  }

}
