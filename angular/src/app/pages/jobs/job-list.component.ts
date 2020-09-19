import { Component, OnInit, ChangeDetectionStrategy } from '@angular/core';
import {
  Protocol,
  WebSocketService,
} from 'src/app/services/web-socket/web-socket.service';
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

  constructor(private webSocketService: WebSocketService) {
    this.webSocketService.connect();
  }

  ngOnInit(): void {
    this.jobList$ = this.webSocketService.getObservable({ type: 'jobs' });
  }
}
