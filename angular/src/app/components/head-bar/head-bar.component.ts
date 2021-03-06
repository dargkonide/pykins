import { Component, OnInit } from '@angular/core';
import { MatIconRegistry } from '@angular/material/icon';
import { DomSanitizer } from '@angular/platform-browser';
import { AuthSocketService } from 'src/app/services/auth-socket/auth-socket.service';
import { AuthenticationService } from 'src/app/services/auth/auth.service';

@Component({
  selector: 'app-head-bar',
  templateUrl: './head-bar.component.html',
  styleUrls: ['./head-bar.component.scss'],
})
export class HeadBarComponent implements OnInit {
  constructor(
    private matIconRegistry: MatIconRegistry,
    private domSanitizer: DomSanitizer,
    public authSocketService: AuthSocketService,
    private authenticationService: AuthenticationService
  ) {
    this.matIconRegistry.addSvgIcon(
      'python',
      this.domSanitizer.bypassSecurityTrustResourceUrl('../assets/python.svg')
    );
  }

  logout(){
    this.authenticationService.logout()
  }

  ngOnInit(): void {}
}
