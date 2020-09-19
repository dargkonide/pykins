import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { JobRoutingModule } from './job-routing.module';
import { ComponentsModule } from 'src/app/components/material.module';
import { MonacoEditorModule } from 'ngx-monaco-editor';
import { FormsModule } from '@angular/forms';

import { CodeComponent } from './code/code.component';
import { VarsComponent } from './vars/vars.component';

@NgModule({
  declarations: [CodeComponent, VarsComponent],
  imports: [
    CommonModule,
    JobRoutingModule,
    ComponentsModule,
    FormsModule,
    MonacoEditorModule,
  ],
})
export class JobModule {}
