import {
  Component,
  OnInit,
  ChangeDetectionStrategy,
  OnDestroy,
} from '@angular/core';
import { Protocol } from 'src/app/services/web-socket/web-socket.service';
import { AuthSocketService } from 'src/app/services/auth-socket/auth-socket.service';
import { Observable, Subscription } from 'rxjs';
import { ActivatedRoute, NavigationEnd, Router } from '@angular/router';
import { filter } from 'rxjs/operators';

export interface IJobList extends Protocol {
  msg?: IJob[];
}
export interface IJob {
  name: string;
  status: string;
}

@Component({
  selector: 'app-jobs',
  templateUrl: './job-list.component.html',
  styleUrls: ['./job-list.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class JobListComponent implements OnInit, OnDestroy {
  jobList$: Observable<IJobList>;
  urlSub: Subscription;

  folderPath: string[];
  currentUrl;

  constructor(
    private authSocketService: AuthSocketService,
    private router: Router,
    private route: ActivatedRoute
  ) {
    this.authSocketService.connect();
  }

  ngOnInit(): void {
    this.currentUrl = this.router.url;
    this.updateJobsList();
    this.urlSub = this.router.events
      .pipe(filter((event) => event instanceof NavigationEnd))
      .subscribe((event: NavigationEnd) => {
        this.currentUrl = event.url;
        this.updateJobsList();
      });
  }

  updateJobsList() {
    this.jobList$ = this.authSocketService.getObservable({
      type: 'jobs',
      folder: decodeURIComponent(this.currentUrl),
    });
  }

  ngOnDestroy(): void {
    this.urlSub.unsubscribe();
  }

  navigate(type: string, name: string): void{
    if(type == 'job') this.router.navigate(['/job/', name]);
    else this.router.navigate([this.currentUrl + '/' + name])
  }
}
