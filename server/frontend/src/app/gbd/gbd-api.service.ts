import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {API_URL} from '../env';

@Injectable()
export class GbdApiService {

  constructor(private http: HttpClient) {
  }

  // GET list of public, future events
  getAllGroups(): Observable<any>{
    return this.http
      .get(`${API_URL}/groups/all`)
  }
}
