import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  docsSidebar: [
    {
      type: 'doc',
      id: 'overview',
      label: 'Overview',
    },
    {
      type: 'category',
      label: 'Install',
      items: [
        {type: 'doc', id: 'installation/macos', label: 'macOS Excel'},
        {type: 'doc', id: 'installation/windows', label: 'Windows Excel'},
      ],
    },
    {
      type: 'category',
      label: 'Use',
      items: [
        {type: 'doc', id: 'usage/excel-quickstart', label: 'Excel Quick Start'},
        {type: 'doc', id: 'usage/example-codes', label: 'Example Codes'},
        {type: 'doc', id: 'usage/review-colors', label: 'Review Colors'},
        {type: 'doc', id: 'usage/python-cli', label: 'Python CLI'},
        {type: 'doc', id: 'usage/troubleshooting', label: 'Troubleshooting'},
      ],
    },
    {
      type: 'category',
      label: 'Technical Details',
      items: [
        {type: 'doc', id: 'technical-details/parser', label: 'Parser Notes'},
        {type: 'doc', id: 'technical-details/scanner-diagnostics', label: 'Scanner Diagnostics'},
      ],
    },
    {
      type: 'category',
      label: 'About',
      items: [
        {type: 'doc', id: 'about/license', label: 'License'},
      ],
    },
  ],
};

export default sidebars;
