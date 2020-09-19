import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DeleteJobDialogComponent } from './delete-job-dialog.component';

describe('DeleteJobDialogComponent', () => {
  let component: DeleteJobDialogComponent;
  let fixture: ComponentFixture<DeleteJobDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DeleteJobDialogComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DeleteJobDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
