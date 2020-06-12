import { Component, OnInit } from '@angular/core';
import { WebSocketService } from 'src/app/core/web-socket/web-socket.service';
import { Observable } from 'rxjs';
import { IJobsList } from 'src/app/pages/jobs/interfaces/IJobsList';




@Component({
  selector: 'app-jobs',
  templateUrl: './jobs.component.html',
  styleUrls: ['./jobs.component.scss']
})
export class JobsComponent implements OnInit {

  jobList$: Observable<IJobsList>

  constructor(private webSocketService: WebSocketService) { }

  ngOnInit(): void {
    this.jobList$ = this.webSocketService.getObservable("jobList")
  }

  sendMessage(event: any){
    this.webSocketService.sendMessage(event.target.value)
  }






}
