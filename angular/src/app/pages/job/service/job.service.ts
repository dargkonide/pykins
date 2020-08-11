import { Injectable } from '@angular/core';
import {CanActivate, Router} from '@angular/router';


@Injectable({
  providedIn: 'root'
})
@Injectable()
export class JobService implements CanActivate {
  constructor(private router: Router) {}

  jobRoute: string;
  jobPath = 'code';
  jobPaths = ['code', 'vars'];

  canActivate(route: any) {
    const target = route.parent._routerState.url.split('/')[4];
    console.log(target, this.jobPath);
    if (this.jobPaths.includes(target) && target != this.jobPath) {
      this.router.navigate([route.parent._routerState.url.replace(target, this.jobPath)]);
      return false;
    }
    return true;
  }


}
