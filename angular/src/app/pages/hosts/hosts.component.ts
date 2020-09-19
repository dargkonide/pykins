import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { WebSocketService } from 'src/app/core/services/web-socket/web-socket.service';

@Component({
  selector: 'app-hosts',
  templateUrl: './hosts.component.html',
  styleUrls: ['./hosts.component.scss'],
})
export class HostsComponent implements OnInit {
  hosts$: Observable<any>;
  hostsSub;

  constructor(private webSocketService: WebSocketService) {
    this.webSocketService.connect();
  }

  ngOnInit(): void {
    this.hosts$ = this.webSocketService.getObservable({ type: 'hosts' });
  }
}
