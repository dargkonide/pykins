import { Component, OnInit, OnDestroy } from '@angular/core';
import { Observable } from 'rxjs';
import { Hosts, WebSocketService } from 'src/app/core/services/web-socket/web-socket.service';

@Component({
  selector: 'app-hosts',
  templateUrl: './hosts.component.html',
  styleUrls: ['./hosts.component.scss']
})
export class HostsComponent implements OnInit, OnDestroy {

  hosts$: Observable<Hosts>;
  hostsSub;

  constructor(
    private webSocketService: WebSocketService
  ) { }

  ngOnInit(): void {
    this.hosts$ = this.webSocketService.getObservable( {type: 'hosts'} );
    this.hostsSub = this.hosts$.subscribe(
      m => console.log(m)
    );
  }

  ngOnDestroy(): void {
    this.hostsSub.unsubscribe();
  }

}
