import { Injectable } from '@angular/core';
import {ActivatedRouteSnapshot, CanActivate, Params} from '@angular/router';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})

export class JobService implements CanActivate {

  jobRoute: string;
  jobPath = 'code';
  canActivate(route: ActivatedRouteSnapshot) {
    return false;
  }

  constructor() { }


}
