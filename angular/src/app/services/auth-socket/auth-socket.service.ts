import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { AuthenticationService } from '../auth/auth.service';
import { IUser } from '../auth/model/user';
import { Protocol, WebSocketService } from '../web-socket/web-socket.service';
import {Router} from '@angular/router';
import { stringify } from '@angular/compiler/src/util';

@Injectable({
  providedIn: 'root',
})
export class AuthSocketService {
  public user: IUser;

  constructor(
    private webSocketService: WebSocketService,
    private authenticationService: AuthenticationService,
    private router: Router
  ) {
    this.authenticationService.user.subscribe(
      (user) => this.user = user
    );
    this.getObservable({type: 'auth_token', token: this.user ? this.user.token : ''})
      .subscribe((m) => {if (!m.auth){
        this.authenticationService.logout(this.router.url); }});
  }
  connect(): void{
    this.webSocketService.connect();
  }
  disconnect(){
    this.webSocketService.disconnect();
  }
  sendMessage(message: Protocol){
    // message.token = this.user.token;
    this.webSocketService.sendMessage(message);
  }
  getObservable(subscribeType: any): Observable<Protocol> {
    // subscribeType.token = this.user.token;
    return this.webSocketService.getObservable(subscribeType);
  }
}
