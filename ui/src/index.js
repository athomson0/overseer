import React from 'react';
import { createRoot } from 'react-dom/client';
import Overseer from './js/App'

const container = document.getElementById('root');
const root = createRoot(container);
root.render(<Overseer />);