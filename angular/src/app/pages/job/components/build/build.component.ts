import { Component, OnInit } from '@angular/core';
import { WebSocketService } from 'src/app/core/services/web-socket/web-socket.service';
import { JobService } from '../../service/job.service';

@Component({
  selector: 'app-build',
  templateUrl: './build.component.html',
  styleUrls: ['./build.component.scss']
})
export class BuildComponent implements OnInit {

  varsSub
  vars

  constructor(
    private webSocketService: WebSocketService,
    private jobService: JobService
  ) { }

  ngOnInit(): void {
    this.varsSub = this.webSocketService.getObservable({
      type:'build',
      name:this.jobService.jobRoute
    }).subscribe(
      m => {
        this.vars = m.msg
        console.log(m)
      }
    )
  }

  runJob(){
    this.webSocketService.sendMessage({
      type:'runJob',
      name:this.jobService.jobRoute,
      vars:this.vars
    })
  }

}
