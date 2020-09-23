import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { AuthenticationService } from '../auth/auth.service';
import { IUser } from '../auth/model/user';
import { Protocol, WebSocketService } from '../web-socket/web-socket.service';

@Injectable({
  providedIn: 'root',
})
export class AuthSocketService {
  public user: IUser

  constructor(
    private webSocketService: WebSocketService,
    private authenticationService: AuthenticationService
  ) {
    this.authenticationService.user.subscribe(
      (user) => this.user = user
    )
  }
  connect(): void{
    this.webSocketService.connect()
  }
  disconnect(){
    this.webSocketService.disconnect()
  }
  sendMessage(message: Protocol){
    message.token = this.user.token
    this.webSocketService.sendMessage(message)
  }
  getObservable(subscribeType: Protocol): Observable<Protocol> {
    subscribeType.token = this.user.token
    return this.webSocketService.getObservable(subscribeType)
  }
}
