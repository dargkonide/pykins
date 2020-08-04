import {Component, OnInit} from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { WebSocketService } from 'src/app/core/services/web-socket/web-socket.service';
import {JobService} from './service/job.service';


@Component({
  selector: 'app-job-page',
  templateUrl: './job-page.component.html',
  styleUrls: ['./job-page.component.scss']
})
export class JobPageComponent implements OnInit {
  jobRoute: string;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    public jobService: JobService,
    public webSocketService: WebSocketService
  ) {

  }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.jobService.jobRoute = params.jobName;
      this.jobRoute = params.jobName;
  });
  }

  navigate(){
    this.webSocketService.sendMessage({
      type: 'name',
      old: this.jobService.jobRoute,
      new: this.jobRoute,
    });
    this.router.navigateByUrl(this.router.url.replace(
        encodeURIComponent(this.jobService.jobRoute),
        encodeURIComponent(this.jobRoute)
        ));
    // replace parameter of navigateByUrl function to your required url
}


}
