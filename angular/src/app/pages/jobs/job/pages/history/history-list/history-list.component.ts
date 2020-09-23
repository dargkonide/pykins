import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { AuthSocketService } from 'src/app/services/auth-socket/auth-socket.service';
import { Protocol } from 'src/app/services/web-socket/web-socket.service';
import { JobService } from '../../../service/job.service';


export interface IHistoryList extends Protocol{
  msg?: IJobHistory[]
}
export interface IJobHistory {
  id: number
  status: string
  start: Date
  end: Date
  delta: Date
}

@Component({
  selector: 'app-history-list',
  templateUrl: './history-list.component.html',
  styleUrls: ['./history-list.component.scss'],
})
export class HistoryListComponent implements OnInit {
  jobHistory$: Observable<IHistoryList>;

  constructor(
    private jobService: JobService,
    private authSocketService: AuthSocketService
  ) {
    // this.authSocketService.connect();
  }

  stop(id): void {
    this.authSocketService.sendMessage({
      type: 'stop',
      name: this.jobService.jobRoute,
      id: id,
    });
  }

  ngOnInit(): void {
    this.jobHistory$ = this.authSocketService.getObservable({
      type: 'history',
      name: this.jobService.jobRoute,
    });
  }
}
