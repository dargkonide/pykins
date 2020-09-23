import { Component } from '@angular/core';
import { AuthSocketService } from './services/auth-socket/auth-socket.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent {
  title = 'pynkins';
  showRouter = false;

  constructor() {}
}
