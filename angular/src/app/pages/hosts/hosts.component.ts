import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { AuthSocketService } from 'src/app/services/auth-socket/auth-socket.service';

@Component({
  selector: 'app-hosts',
  templateUrl: './hosts.component.html',
  styleUrls: ['./hosts.component.scss'],
})
export class HostsComponent implements OnInit {
  hosts$: Observable<any>;
  hostsSub;

  constructor(private authSocketService: AuthSocketService) {
    this.authSocketService.connect();
  }

  ngOnInit(): void {
    this.hosts$ = this.authSocketService.getObservable({ type: 'hosts' });
  }
}
