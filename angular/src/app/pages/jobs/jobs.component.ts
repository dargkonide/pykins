import { Component, OnInit, ViewChild } from '@angular/core';
import { WebSocketService } from 'src/app/core/services/web-socket/web-socket.service';
import { Observable } from 'rxjs';
import { IJobsList, IRows } from 'src/app/pages/jobs/interfaces/IJobsList';
import { MatTableDataSource } from '@angular/material/table';
import { MatSort } from '@angular/material/sort';

@Component({
  selector: 'app-jobs',
  templateUrl: './jobs.component.html',
  styleUrls: ['./jobs.component.scss']
})
export class JobsComponent implements OnInit {

  jobList$: Observable<IJobsList>

  displayedColumns: string[] = ['name', 'status'];
  dataSource: MatTableDataSource<IRows>

  @ViewChild(MatSort, {static: true}) sort: MatSort;

  constructor(private webSocketService: WebSocketService) {
    this.jobList$ = this.webSocketService.getObservable("jobList")
    this.jobList$.subscribe(
      message => {
        console.log(message)
        this.dataSource = new MatTableDataSource(message.table)
      }
    )
   }

  ngOnInit(): void {
    this.dataSource.sort = this.sort;
  }

  reconnect(){
    this.webSocketService.ws.unsubscribe()
    if (this.webSocketService.ws.isStopped){
      console.log('WebSocket stopped')

    }

  }

  sendMessage(event: any){
    this.webSocketService.sendMessage(event.target.value)
  }






}
