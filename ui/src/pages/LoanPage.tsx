import React, { useState } from 'react';
import LoanForm from '../components/loan-form';
import LoanDisplay from '../components/loan-display';

const LoanPage: React.FC = () => {
    const [loanResult, setLoanResult] = useState<{
        monthly_payment: string,
        id?: number,
        loan_amount?: string,
        interest_rate?: string,
        loan_term?: string
        customer?: null | object
    }>({
        monthly_payment: "0",
    });

    const handleLoanSubmit = (loanData: {
        monthly_payment: string,
        id: number,
        loan_amount: string,
        interest_rate: string,
        loan_term: string
        customer: null | object
    }) => {
        setLoanResult(loanData);
    };

    return (
        <div>
            <h1>Loan Calculator</h1>
            <LoanForm onLoanSubmit={handleLoanSubmit} />
            <LoanDisplay loanData={loanResult} />
        </div>
    );
};

export default LoanPage;

