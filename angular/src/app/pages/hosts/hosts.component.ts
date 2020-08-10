import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { Hosts, WebSocketService } from 'src/app/core/services/web-socket/web-socket.service';

@Component({
  selector: 'app-hosts',
  templateUrl: './hosts.component.html',
  styleUrls: ['./hosts.component.scss']
})
export class HostsComponent implements OnInit {

  hosts$: Observable<Hosts>;

  constructor(
    private webSocketService: WebSocketService
  ) { }

  ngOnInit(): void {
    this.hosts$ = this.webSocketService.getObservable( {type: 'hosts'} );
    this.hosts$.subscribe(
      m => console.log(m)
    );
  }

}
