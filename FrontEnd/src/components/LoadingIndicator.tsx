/** @jsxImportSource @emotion/react */

import { css, keyframes } from '@emotion/react';

const bounceDelay = keyframes`
    0%, 80%, 100% { 
        transform: scale(0);
    } 40% { 
        transform: scale(1.0);
    }
`;

const spinnerDot = css`
    display: inline-block;
    border-radius: 100%;
    width: 12px;
    height: 12px;
    margin: 6px;
    background-color: #333;
    animation: ${bounceDelay} infinite 1.4s ease-in-out both;
`;

const spinner = css`
    display: inline-block;
    text-align: center;
`;
export default function LoadingIndicator() {
    return (
        <div css={spinner}>
            <div css={spinnerDot} />
            <div css={spinnerDot} />
            <div css={spinnerDot} />
        </div>
    );
}