import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { HostsRoutingModule } from './hosts-routing.module';
import { HostsComponent } from './hosts.component';
import { MaterialModule } from 'src/app/util/material/material.module';


@NgModule({
  declarations: [HostsComponent],
  imports: [
    CommonModule,
    HostsRoutingModule,
    MaterialModule
  ]
})
export class HostsModule { }
