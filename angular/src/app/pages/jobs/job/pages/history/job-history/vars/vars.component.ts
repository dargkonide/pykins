import { Component, OnInit, ViewChild } from '@angular/core';
import { JobService } from 'src/app/pages/jobs/job/service/job.service';
import { AuthSocketService } from 'src/app/services/auth-socket/auth-socket.service';

@Component({
  selector: 'app-vars',
  templateUrl: './vars.component.html',
  styleUrls: ['./vars.component.scss'],
})
export class VarsComponent implements OnInit {
  varsSub;
  vars;

  constructor(
    private authSocketService: AuthSocketService,
    private jobService: JobService
  ) {
    this.authSocketService.connect();
  }

  ngOnInit(): void {
    this.varsSub = this.authSocketService
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
    this.authSocketService.sendMessage({
      type: 'change_vars',
      name: this.jobService.jobRoute,
      id: location.pathname.split('/')[4],
      vars: this.vars,
    });
  }
}
