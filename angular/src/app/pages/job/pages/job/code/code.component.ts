import { Component, OnInit, OnDestroy } from '@angular/core';
import { WebSocketService } from 'src/app/core/services/web-socket/web-socket.service';
import { JobService } from '../../../service/job.service';
import { JobComponent } from '../job.component';

@Component({
  selector: 'app-code',
  templateUrl: './code.component.html',
  styleUrls: ['./code.component.scss'],
})
export class CodeComponent implements OnInit, OnDestroy {
  // https://www.npmjs.com/package/ngx-monaco-editor
  editorOptions = {
    theme: 'vs-dark',
    language: 'python',
    automaticLayout: true,
    forceMoveMarkers: false,
  };
  jobCodeSub;
  jobCode;

  constructor(
    public webSocketService: WebSocketService,
    public jobService: JobService,
    public jobComponent: JobComponent
  ) {
    this.webSocketService.connect();
  }

  ngOnInit(): void {
    this.jobService.jobPath = 'code';
    this.jobComponent.activeLink = 'code';
    this.jobCodeSub = this.webSocketService
      .getObservable({
        type: 'getCode',
        name: this.jobService.jobRoute,
      })
      .subscribe((m) => (this.jobCode = m.code));
  }

  ngOnDestroy(): void {
    this.jobCodeSub.unsubscribe();
  }

  sendChangedCode() {
    this.webSocketService.sendMessage({
      type: 'setCode',
      name: this.jobService.jobRoute,
      code: this.jobCode,
    });
  }
}
