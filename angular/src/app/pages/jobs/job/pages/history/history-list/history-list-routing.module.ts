import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from 'src/app/services/auth/AuthGuard';
import { HistoryListComponent } from './history-list.component';

const routes: Routes = [
  { path: '', canActivate: [AuthGuard], component: HistoryListComponent },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class HistoryListRoutingModule {}
