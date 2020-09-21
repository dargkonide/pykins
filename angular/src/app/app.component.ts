import { Component } from '@angular/core';
import { AuthenticationService } from './services/auth/auth.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent {
  title = 'pynkins';
  user;
  showRouter = false;

  constructor(private authenticationService: AuthenticationService) {
    this.authenticationService.user.subscribe((user) => (this.user = user));
  }
}
