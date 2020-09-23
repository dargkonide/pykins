import { TestBed } from '@angular/core/testing';

import { AuthSocketService } from './auth-socket.service';

describe('AuthSocketService', () => {
  let service: AuthSocketService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AuthSocketService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
