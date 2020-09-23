import { Component, OnInit } from '@angular/core';
import { AuthSocketService } from 'src/app/services/auth-socket/auth-socket.service';
import { JobService } from '../../service/job.service';

@Component({
  selector: 'app-delete-job-dialog',
  templateUrl: './delete-job-dialog.component.html',
  styleUrls: ['./delete-job-dialog.component.scss'],
})
export class DeleteJobDialogComponent implements OnInit {
  constructor(
    public jobService: JobService,
    public authSocketService: AuthSocketService
  ) {
    this.authSocketService.connect();
  }

  ngOnInit(): void {}

  deleteJob() {
    this.authSocketService.sendMessage({
      type: 'delete',
      name: this.jobService.jobRoute,
    });
  }
}
