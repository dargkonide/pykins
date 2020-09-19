import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { ActivatedRoute, Router } from '@angular/router';
import { WebSocketService } from 'src/app/services/web-socket/web-socket.service';
import { DeleteJobDialogComponent } from './pages/delete-job-dialog/delete-job-dialog.component';
import { JobService } from './service/job.service';

@Component({
  selector: 'app-job-page',
  templateUrl: './job-page.component.html',
  styleUrls: ['./job-page.component.scss'],
})
export class JobPageComponent implements OnInit {
  jobRoute: string;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    public jobService: JobService,
    public webSocketService: WebSocketService,
    public dialog: MatDialog
  ) {
    this.webSocketService.connect();
  }

  ngOnInit(): void {
    this.route.params.subscribe((params) => {
      this.jobService.jobRoute = decodeURIComponent(params.jobName);
      this.jobRoute = decodeURIComponent(params.jobName);
    });
  }

  navigate() {
    this.webSocketService.sendMessage({
      type: 'name',
      old: this.jobService.jobRoute,
      new: this.jobRoute,
    });
    this.router.navigateByUrl(
      this.router.url.replace(
        encodeURIComponent(this.jobService.jobRoute),
        encodeURIComponent(this.jobRoute)
      )
    );
  }

  deleteJobDialog() {
    this.dialog.open(DeleteJobDialogComponent);
  }
}
