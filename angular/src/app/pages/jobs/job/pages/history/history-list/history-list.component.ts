import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { Protocol, WebSocketService } from 'src/app/services/web-socket/web-socket.service';
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
  jobHistory$: Observable<IHistoryList>

  constructor(
    private jobService: JobService,
    private webSocketService: WebSocketService
  ) {
    this.webSocketService.connect();
  }

  ngOnInit(): void {
    this.jobHistory$ = this.webSocketService.getObservable({
      type: 'history',
      name: this.jobService.jobRoute,
    });
  }
}
