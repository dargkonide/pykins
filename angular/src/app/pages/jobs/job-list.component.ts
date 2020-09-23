import { Component, OnInit, ChangeDetectionStrategy } from '@angular/core';
import {
  Protocol,
} from 'src/app/services/web-socket/web-socket.service';
import { AuthSocketService } from 'src/app/services/auth-socket/auth-socket.service';
import { Observable } from 'rxjs';

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
export class JobListComponent implements OnInit {
  jobList$: Observable<IJobList>;

  constructor(private authSocketService: AuthSocketService) {
    this.authSocketService.connect();
  }

  ngOnInit(): void {
    this.jobList$ = this.authSocketService.getObservable({ type: 'jobs' });
  }
}
