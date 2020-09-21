import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { WebSocketService } from '../web-socket/web-socket.service';

import { IAuth, IUser } from './model/user';

@Injectable({ providedIn: 'root' })
export class AuthenticationService {
  private userSubject: BehaviorSubject<IUser>;
  public user: Observable<IUser>;

  constructor(
    private router: Router,
    private webSocketService: WebSocketService // private http: HttpClient
  ) {
    this.userSubject = new BehaviorSubject<IUser>(
      JSON.parse(localStorage.getItem('user'))
    );
    this.user = this.userSubject.asObservable();
  }

  public get userValue(): IUser {
    return this.userSubject.value;
  }

  login(username: string, password: string) {
    return this.webSocketService
      .getObservable({ type: 'authenticate', user: username, pass: password })
      .pipe(
        map((resp) => {
          console.debug(resp)
          // store user details and jwt token in local storage to keep user logged in between page refreshes
          localStorage.setItem('user', JSON.stringify(resp.msg));
          this.userSubject.next(resp.msg);
          return resp.msg;
        })
      );
  }

  logout() {
    // remove user from local storage to log user out
    localStorage.removeItem('user');
    this.userSubject.next(null);
    this.router.navigate(['/login']);
  }
}
