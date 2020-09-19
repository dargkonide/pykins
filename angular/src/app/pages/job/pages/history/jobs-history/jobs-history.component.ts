import { Component, OnInit } from '@angular/core';
import { WebSocketService } from 'src/app/core/services/web-socket/web-socket.service';
import { JobService } from '../../../service/job.service';

@Component({
  selector: 'app-jobs-history',
  templateUrl: './jobs-history.component.html',
  styleUrls: ['./jobs-history.component.scss'],
})
export class JobsHistoryComponent implements OnInit {
  jobHistory$;

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
