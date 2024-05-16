import { motion } from 'framer-motion';
import { slideFromLeftAnimationVariants, textAnimationVariants } from '../static/variants';
export default function About() {
    return (
        <article className="h-full w-full">
            <section className="bg-family h-screen w-full bg-center bg-cover relative">
                <div className="h-full w-full bg-gradient-to-r from-10% from-white via-60% via-transparent"></div>
                <motion.div
                    className="text-[calc(4vw+1em)] font-semibold absolute top-[25%] max-md:text-center max-md:w-full px-12 text-pacific-blue leading-tight cursor-default"
                    initial="initial"
                    animate="animate"
                    exit="exit"
                    transition={{ ease: 'easeOut', duration: 0.5 }}
                    variants={slideFromLeftAnimationVariants}>
                    Lorem ipsum dolor.
                    <br />
                    Lorem Ipsum
                    <br />
                    <div className="text-[#262626] leading-tight text-[0.5em]">something</div>
                    <button
                        className="text-white bg-pacific-blue text-[0.3em] font-normal max-md:text-[0.4em] px-8 py-4 max-md:py-3 mt-5 rounded-md max-ms:w-full shadow-xl max-ms:drop-shadow-lg z-40 transition ease-in-out hover:scale-105"
                        onClick={() => (window.location.href = '/')}>
                        Get Started
                    </button>
                </motion.div>
            </section>
            <section className="bg-pacific-blue from-10% bg-gradient-to-t from-[#19182f42] min-h-screen h-full w-full bg-center bg-cover relative py-10 justify-center items-center">
                <motion.header
                    className="flex self-center justify-center items-stretch text-pacific-light-gray font-semibold text-[calc(2vw+2em)] mb-6 text-center"
                    initial="initial"
                    whileInView="animate"
                    viewport={{ once: true }}
                    exit="exit"
                    variants={textAnimationVariants}
                    transition={{ ease: 'easeOut', duration: 0.5, delay: 0.2 }}>
                    What is our project about?
                </motion.header>
            </section>

            <section className="bg-pacific-light-gray min-h-screen h-full w-full bg-center bg-cover relative py-10 justify-center items-center">
                <motion.header
                    className="flex self-center justify-center items-stretch text-pacific-blue font-semibold text-[calc(2vw+2em)] mb-6"
                    initial="initial"
                    whileInView="animate"
                    viewport={{ once: true }}
                    exit="exit"
                    variants={textAnimationVariants}
                    transition={{ ease: 'easeOut', duration: 0.5, delay: 0.2 }}>
                    What we've achieved
                </motion.header>
                <motion.div
                    className="flex h-full flex-wrap flex-row justify-center"
                    initial="initial"
                    whileInView="animate"
                    viewport={{ once: true }}
                    exit="exit"
                    variants={textAnimationVariants}
                    transition={{ ease: 'easeOut', duration: 0.5, delay: 0.5 }}>
                    <div className="from-transparent to-transparent text-pacific-blue flex md:flex-half md:h-[40vh] md:border-r md:border-b md:max-h-[400px] w-full h-[33vh] max-md:border-b border-pacific-blue items-center justify-center text-center transition ease-in-out hover:bg-pacific-blue  hover:text-pacific-light-gray">
                        <div className="flex flex-col">
                            <div className="text-4xl font-semibold">Something</div>
                            <div>Something</div>
                            <div>Something</div>
                        </div>
                    </div>
                    <div className="from-transparent to-transparent text-pacific-blue flex md:flex-half md:h-[40vh] md:border-l md:border-b md:max-h-[400px] w-full h-[33vh] max-md:border-b border-pacific-blue items-center justify-center text-center transition ease-in-out hover:bg-pacific-blue  hover:text-pacific-light-gray">
                        <div className="flex flex-col">
                            <div className="text-4xl font-semibold">Something</div>
                            <div>Something</div>
                            <div>Something</div>
                        </div>
                    </div>
                    <div className="from-transparent to-transparent text-pacific-blue flex md:flex-half md:h-[40vh] md:border-r md:border-t md:max-h-[400px] w-full h-[33vh] max-md:border-b border-pacific-blue items-center justify-center text-center transition ease-in-out hover:bg-pacific-blue  hover:text-pacific-light-gray">
                        <div className="flex flex-col">
                            <div className="text-4xl font-semibold">Something</div>
                            <div>Something</div>
                            <div>Something</div>
                        </div>
                    </div>
                    <div className="from-transparent to-transparent text-pacific-blue flex md:flex-half md:h-[40vh] md:border-l md:border-t md:max-h-[400px] w-full h-[33vh] border-pacific-blue items-center justify-center text-center transition ease-in-out hover:bg-pacific-blue  hover:text-pacific-light-gray">
                        <div className="flex flex-col">
                            <div className="text-4xl font-semibold">Something</div>
                            <div>Something</div>
                            <div>Something</div>
                        </div>
                    </div>
                </motion.div>
            </section>
            <footer className="bg-black h-[10vh] text-pacific-light-gray text-center">Footer</footer>
        </article>
    );
}
