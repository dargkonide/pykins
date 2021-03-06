import { Component, OnDestroy, OnInit } from '@angular/core';
import { AuthSocketService } from 'src/app/services/auth-socket/auth-socket.service';
import { JobService } from '../../../service/job.service';
import { JobComponent } from '../job.component';

@Component({
  selector: 'app-vars',
  templateUrl: './vars.component.html',
  styleUrls: ['./vars.component.scss'],
})
export class VarsComponent implements OnInit, OnDestroy {
  // https://www.npmjs.com/package/ngx-monaco-editor
  editorOptions = {
    theme: 'vs-dark',
    language: 'python',
    automaticLayout: true,
    forceMoveMarkers: false,
  };
  jobVars;
  jobVarsSub;

  constructor(
    public authSocketService: AuthSocketService,
    public jobService: JobService,
    public jobComponent: JobComponent
  ) {
    this.authSocketService.connect();
  }

  ngOnInit(): void {
    this.jobService.jobPath = 'vars';
    this.jobComponent.activeLink = 'vars';
    this.jobVarsSub = this.authSocketService
      .getObservable({
        type: 'getVars',
        name: this.jobService.jobRoute,
      })
      .subscribe((m) => (this.jobVars = m.vars));
  }

  ngOnDestroy(): void {
    this.jobVarsSub.unsubscribe();
  }

  sendChangedVars() {
    this.authSocketService.sendMessage({
      type: 'setVars',
      name: this.jobService.jobRoute,
      vars: this.jobVars,
    });
  }
}
