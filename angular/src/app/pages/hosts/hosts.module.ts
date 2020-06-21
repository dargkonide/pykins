import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { HostsRoutingModule } from './hosts-routing.module';
import { HostsComponent } from './hosts.component';


@NgModule({
  declarations: [HostsComponent],
  imports: [
    CommonModule,
    HostsRoutingModule
  ]
})
export class HostsModule { }
