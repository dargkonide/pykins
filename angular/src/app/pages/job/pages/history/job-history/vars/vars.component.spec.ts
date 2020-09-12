import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { VarsComponent } from './vars.component';

describe('VarsComponent', () => {
  let component: VarsComponent;
  let fixture: ComponentFixture<VarsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ VarsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(VarsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
