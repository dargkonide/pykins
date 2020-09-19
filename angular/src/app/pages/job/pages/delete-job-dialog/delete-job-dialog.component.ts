import { Component, OnInit } from '@angular/core';
import { WebSocketService } from 'src/app/core/services/web-socket/web-socket.service';
import { JobService } from '../../service/job.service';

@Component({
  selector: 'app-delete-job-dialog',
  templateUrl: './delete-job-dialog.component.html',
  styleUrls: ['./delete-job-dialog.component.scss'],
})
export class DeleteJobDialogComponent implements OnInit {
  constructor(
    public jobService: JobService,
    public webSocketService: WebSocketService
  ) {
    this.webSocketService.connect();
  }

  ngOnInit(): void {}

  deleteJob() {
    this.webSocketService.sendMessage({
      type: 'delete',
      name: this.jobService.jobRoute,
    });
  }
}
