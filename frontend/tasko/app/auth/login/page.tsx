import Login from '@/pages/auth/Login';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Authentication | Log In',
  description: 'Log In page for authentication.',
  appleWebApp: {
    title: "Tasko",
    capable: true,
    statusBarStyle: "default",
  }
};

export default function Page() {
  
  return <Login />;

}