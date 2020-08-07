import { NgModule } from '@angular/core';
import {Routes, RouterModule, Router} from '@angular/router';
import {JobComponent} from './job.component';
import {JobService} from '../../service/job.service';
import { CodeComponent } from './code/code.component';
import { VarsComponent } from './vars/vars.component';


export let routes: Routes = [{
  path: '', component: JobComponent,
  children: [
    { path: '', redirectTo: 'code'},

    {path: 'code', component: CodeComponent},
    {path: 'vars', component: VarsComponent},

    { path: '**', redirectTo: '' },

  ]
 }];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class JobRoutingModule {
}
