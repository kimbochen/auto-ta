import { ReactWidget } from '@jupyterlab/ui-components';
import React from 'react';


export class TABotWidget extends ReactWidget {
  constructor() {
    super();
    this.addClass('jp-react-widget');
  }

  render(): JSX.Element {
    return (
      <iframe
        src="http://localhost:8888"  // PORT
        title="Auto TA"
        frameBorder="0"
        allowFullScreen
        style={{ width: '1200px', height: '580px' }}
      />
    );
  }
}
