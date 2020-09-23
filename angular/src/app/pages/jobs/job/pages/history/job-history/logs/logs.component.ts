import { Component, OnInit, OnDestroy } from '@angular/core';
import { AuthSocketService } from 'src/app/services/auth-socket/auth-socket.service';
import { JobService } from '../../../../service/job.service';

@Component({
  selector: 'app-logs',
  templateUrl: './logs.component.html',
  styleUrls: ['./logs.component.scss'],
})
export class LogsComponent implements OnInit, OnDestroy {
  editorOptions = {
    theme: 'vs-dark',
    language: 'python',
    automaticLayout: true,
    forceMoveMarkers: false,
    wordWrap: 'off',
    readOnly: true,
    scrollBeyondLastLine: true,
  };
  jobLogsSub;
  jobLogsUpdateSub;
  jobLogs;

  constructor(
    public authSocketService: AuthSocketService,
    public jobService: JobService
  ) {
    this.authSocketService.connect();
  }

  ngOnInit(): void {
    this.jobLogsSub = this.authSocketService
      .getObservable({
        type: 'getLogs',
        id: location.pathname.split('/')[4],
        name: this.jobService.jobRoute,
      })
      .subscribe((m) => (this.jobLogs = m.logs));
    this.jobLogsUpdateSub = this.authSocketService
      .getObservable({
        type: 'glu',
        id: location.pathname.split('/')[4],
        name: this.jobService.jobRoute,
      })
      .subscribe((m) => (this.jobLogs = this.jobLogs + '\n' + m.logs));
  }

  ngOnDestroy(): void {
    this.jobLogsSub.unsubscribe();
    this.jobLogsUpdateSub.unsubscribe();
  }
}
