import '@testing-library/jest-dom';
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import LoanForm from './index';

describe('LoanForm Component', () => {
  it('renders the form inputs and submit button', () => {
    const mockSubmit = jest.fn();
    render(<LoanForm onLoanSubmit={mockSubmit} />);

    expect(screen.getByPlaceholderText('Loan Amount')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Interest Rate (%)')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Loan Term (months)')).toBeInTheDocument();
    
    expect(screen.getByRole('button', { name: /submit/i })).toBeInTheDocument();
  });
});
