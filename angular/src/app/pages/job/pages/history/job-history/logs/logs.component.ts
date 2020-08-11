import { Component, OnInit, OnDestroy } from '@angular/core';
import { WebSocketService } from 'src/app/core/services/web-socket/web-socket.service';
import { JobService } from '../../../../service/job.service';


@Component({
  selector: 'app-logs',
  templateUrl: './logs.component.html',
  styleUrls: ['./logs.component.scss']
})
export class LogsComponent implements OnInit, OnDestroy {

  editorOptions = { theme: 'vs-dark', language: 'python', automaticLayout: true, forceMoveMarkers: false };
  jobLogsSub;
  jobLogsUpdateSub;
  jobLogs;

  constructor(public webSocketService: WebSocketService,
              public jobService: JobService) { }

  ngOnInit(): void {
    this.jobLogsSub = this.webSocketService.getObservable({
      type: 'getLogs',
      id: location.pathname.split('/')[5],
      name: this.jobService.jobRoute
    }).subscribe(
      m => this.jobLogs = m.logs
    );
    this.jobLogsUpdateSub = this.webSocketService.getObservable({
      type: 'glu',
      id: location.pathname.split('/')[5],
      name: this.jobService.jobRoute
    }).subscribe(
      m => this.jobLogs = this.jobLogs + '\n' + m.logs
    );
  }

  ngOnDestroy(): void {
    this.jobLogsSub.unsubscribe();
    this.jobLogsUpdateSub.unsubscribe();
  }

}
