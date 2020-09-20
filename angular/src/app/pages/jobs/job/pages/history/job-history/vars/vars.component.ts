import { Component, OnInit, ViewChild } from '@angular/core';
import { WebSocketService } from 'src/app/services/web-socket/web-socket.service';
import { JobService } from 'src/app/pages/jobs/job/service/job.service';

@Component({
  selector: 'app-vars',
  templateUrl: './vars.component.html',
  styleUrls: ['./vars.component.scss'],
})
export class VarsComponent implements OnInit {
  varsSub;
  vars;

  constructor(
    private webSocketService: WebSocketService,
    private jobService: JobService
  ) {
    this.webSocketService.connect();
  }

  ngOnInit(): void {
    this.varsSub = this.webSocketService
      .getObservable({
        type: 'build',
        name: this.jobService.jobRoute,
      })
      .subscribe((m) => {
        this.vars = m.msg;
        console.log(m);
      });
  }

  ngOnDestroy(): void {
    this.varsSub.unsubscribe();
  }

  confirm() {
    this.webSocketService.sendMessage({
      type: 'change_vars',
      name: this.jobService.jobRoute,
      id: location.pathname.split('/')[4],
      vars: this.vars,
    });
  }
}
