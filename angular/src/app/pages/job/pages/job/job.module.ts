import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { JobRoutingModule } from './job-routing.module';
import { CodeComponent } from './code/code.component';
import { VarsComponent } from './vars/vars.component';
import { MaterialModule } from 'src/app/util/material/material.module';
import { MonacoEditorModule } from 'ngx-monaco-editor';
import { FormsModule } from '@angular/forms';


@NgModule({
  declarations: [CodeComponent, VarsComponent],
  imports: [
    CommonModule,
    JobRoutingModule,
    MaterialModule,
    FormsModule,
    MonacoEditorModule
  ]
})
export class JobModule { }
