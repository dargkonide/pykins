import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { HostsRoutingModule } from './hosts-routing.module';
import { HostsComponent } from './hosts.component';
import { ComponentsModule } from 'src/app/components/material.module';


@NgModule({
  declarations: [HostsComponent],
  imports: [
    CommonModule,
    HostsRoutingModule,
    ComponentsModule
  ]
})
export class HostsModule { }
